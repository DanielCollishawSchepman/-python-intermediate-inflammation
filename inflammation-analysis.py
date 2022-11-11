#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse

from inflammation import models, views, serializers


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    infiles = args.infiles
    if not isinstance(infiles, list):
        infiles = [args.infiles]

    for filename in infiles:

        if args.view == 'visualize':
            inflammation_data = models.load_csv(filename)
            view_data = {
                'average': models.daily_mean(inflammation_data),
                'max': models.daily_max(inflammation_data),
                'min': models.daily_min(inflammation_data),
            }

            views.visualize(view_data)

        elif args.view == 'record':
            inflammation_data = models.load_csv(filename)
            patient_data = inflammation_data[args.patient]
            observations = [models.Observation(day, value) for day, value in enumerate(patient_data)]
            patient = models.Patient('UNKNOWN', observations)

            views.display_patient_record(patient)

        elif args.view == 'list-patients':
            if args.serializer == "json":
                records = serializers.PatientJSONSerializer.load(filename)
            elif args.serializer == "csv":
                records = serializers.PatientCSVSerializer.load(filename)

            views.display_patients_list(records)
        
        elif args.view == 'new-patient':
            if args.serializer == "json":
                records = serializers.PatientJSONSerializer.load(filename)
            elif args.serializer == "csv":
                records = serializers.PatientCSVSerializer.load(filename)

            records += [models.Patient(args.patientname)]

            if args.serializer == "json":
                serializers.PatientJSONSerializer.save(records, filename)
            elif args.serializer == "csv":
                serializers.PatientCSVSerializer.save(records, filename)
            views.display_patients_list(records)


        elif args.view == 'new-observation':
            if args.serializer == "json":
                records = serializers.PatientJSONSerializer.load(filename)
            elif args.serializer == "csv":
                records = serializers.PatientCSVSerializer.load(filename)

            if args.patientname not in [record.name for record in records]:
                raise KeyError(f"Patient {args.patientname} not found.")

            for record in records:
                if record.name == args.patientname:
                    record.add_observation(args.observation)
                    views.display_patient_record(record)

            if args.serializer == "json":
                serializers.PatientJSONSerializer.save(records, filename)
                
            elif args.serializer == "csv":
                serializers.PatientCSVSerializer.save(records, filename)
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A basic patient inflammation data management system')

    parser.add_argument(
        'infiles',
        nargs='+',
        help='Input CSV(s) containing inflammation series for each patient'
        )

    parser.add_argument(
        '--view',
        default='visualize',
        choices=['visualize', 'record', 'list-patients', 'new-patient', 'new-observation'],
        help='Which view should be used?')

    parser.add_argument(
        '--patient',
        type=int,
        default=0,
        help='Which patient should be displayed?')

    parser.add_argument(
        '--patientname',
        help='Which patient should be displayed?')

    parser.add_argument(
        '--observation',
        help='What is the value of the observation to be added?')

    parser.add_argument(
        '--serializer',
        default='json',
        choices=['json', 'csv'],
        help='What serializer should be used?')

    args = parser.parse_args()

    main(args)
