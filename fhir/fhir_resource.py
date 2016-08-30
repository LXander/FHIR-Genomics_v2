'''
    The aim for this file is to find a way to make a sophisticated class to generate and parse resource in fhir

    we think fhir resource have 4 layer:

    basic element : e.g. code (string), decimal (float)

    components : e.g. CodeableConcept, Extension

    Sets of components: e.g. ValueSet, CodeSystem, BackBoneElement

    Resource itself: Patient, etc.

    The function needs to finish the following tasks:

    with a template of definition, can it parse or check a resource correctly?

'''