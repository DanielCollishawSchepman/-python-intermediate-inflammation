from inflammation import models

from abc import ABC, abstractmethod
import json
import csv


class Serializer(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, instances):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def save(cls, instances, path):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path):
        raise NotImplementedError


class ObservationSerializer(Serializer):
    model = models.Observation

    @classmethod
    def serialize(cls, instances):
        return [{
            'day': instance.day,
            'value': instance.value,
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        return [cls.model(**d) for d in data]


class PatientSerializer:
    model = models.Patient

    @classmethod
    def serialize(cls, instances):
        return [{
            'name': instance.name,
            'observations': ObservationSerializer.serialize(instance.observations),
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        instances = []

        for item in data:
            item['observations'] = ObservationSerializer.deserialize(item.pop('observations'))
            instances.append(cls.model(**item))

        return instances


class PatientJSONSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)

    @classmethod
    def load(cls, path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialize(data)


class PatientCSVSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
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
