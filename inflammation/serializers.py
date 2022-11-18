from inflammation import models

from abc import ABC, abstractmethod
import json
import csv


class Serializer(ABC):
    """ Abstract Base Class (ABC), only used by creating
        subclasses of it. Templates for other serializers,
        and will give an error if templates are not used
        for other serializers.
    """

    @classmethod
    @abstractmethod
    def serialize(cls, instances):
        """ Serialize template """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def save(cls, instances, path):
        """ Save template """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, data):
        """ Deserialize template """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path):
        """ Load template """
        raise NotImplementedError


class ObservationSerializer(Serializer):
    model = models.Observation
    """ Serialize and deserialize Observation
        objects using Serializer templates.
    """

    @classmethod
    def serialize(cls, instances):
        """ Serializes """
        return [{
            'day': instance.day,
            'value': instance.value,
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        """ Deserializes """
        return [cls.model(**d) for d in data]


class PatientSerializer:
    model = models.Patient
    """ Serialize and deserialize Patient
        objects using Serializer templates.
    """

    @classmethod
    def serialize(cls, instances):
        """ Serializes """
        return [{
            'name': instance.name,
            'observations': ObservationSerializer.serialize(instance.observations),
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        """ Deserializes """
        instances = []

        for item in data:
            item['observations'] = ObservationSerializer.deserialize(item.pop('observations'))
            instances.append(cls.model(**item))

        return instances


class PatientJSONSerializer(PatientSerializer):
    """ Serializes patient for JSON """
    @classmethod
    def save(cls, instances, path):
        """ Saves """
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)

    @classmethod
    def load(cls, path):
        """ Loads """
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialize(data)


class PatientCSVSerializer(PatientSerializer):
    """ Serializes patient for VCSV """
    @classmethod
    def save(cls, instances, path):
        """ Saves """
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            records = cls.serialize(instances)
            for patient in records:
                if patient["observations"] == []:
                    writer.writerow([patient["name"]])
                else:
                    data = [[patient["name"]]]
                    data += [[int(dicti["day"]), int(dicti["value"])] for dicti in patient["observations"]]
                    data = [item for sublist in data for item in sublist]
                    writer.writerow(data)


    @classmethod
    def load(cls, path):
        """ Loads """
        data = []
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 2:
                    data += [{
                        "name": row[0],
                        "observations": []
                    }]
                    continue

                record = [{
                        "name": row[0],
                        "observations": [{"day": int(row[i]), "value": int(row[i+1])} for i in range(1, len(row) - 1, 2)]
                    }]

                data += record

        return cls.deserialize(data)
