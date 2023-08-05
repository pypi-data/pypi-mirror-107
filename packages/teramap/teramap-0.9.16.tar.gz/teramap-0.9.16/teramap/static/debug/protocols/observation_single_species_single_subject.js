/* eslint-disable no-unused-vars, quotes */

var data = {
    protocol: {
        name: 'Instippen (observation)',
        pinpoint_target: 'observation',
        species: {
            '207': {pk: 207, name: 'Ivoormeeuw', group: 1}
        },
        subjects: {
            '24': 'adult man',
        },
        groups: {
            1: {
                pk: 1,
                name: 'Birds',
                subjects: [24, ]
            }
        }
    },
    initial_data: [
        {"observations": [
            {
                "name": "1",
                pk: 2,
                "latlng": [50.98, -0.089],
                "species": 207,
                "subject": 24,
                "count": 23
            }
        ]}
    ]
};
