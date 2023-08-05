import unittest
from htl.htl import hierarchical_to_linear, linear_to_hierarchical


class HTLTest(unittest.TestCase):

    linear_1 = [
        {'name': 'Lorem',       'parent': None},
        {'name': 'ipsum',       'parent': 'Lorem'},
        {'name': 'dolor',       'parent': 'ipsum'},
        {'name': 'sit',         'parent': 'dolor'},
        {'name': 'amet',        'parent': 'ipsum'},
        {'name': 'consectetur', 'parent': 'Lorem'},
        {'name': 'adipisicing', 'parent': 'consectetur'}
    ]

    hierarchical_1 = {
        'name': 'Lorem',
        'children': [
                {
                    'name': 'ipsum',
                    'children': [
                        {
                            'name': 'dolor',
                            'children': [
                                {
                                    'name': 'sit'
                                }
                            ]
                        },
                        {
                            'name': 'amet'
                        }
                    ]
                },
            {
                    'name': 'consectetur',
                    'children': [
                        {
                            'name': 'adipisicing'
                        }
                    ]
            }
        ]
    }

    hierarchical__2 = {
        'name': 'Pets',
        'children': [
            {
                'name': 'Dogs',
                'children': [
                    {
                        'name': 'Poodle'
                    },
                    {
                        'name': 'Dalmatian'
                    }, 
                    {
                        'name': 'Husky'
                    }
                ]
            }, 
            {
                'name': 'Cats',
                'children': [
                    {
                        'name': 'Siamse'
                    },
                    {
                        'name': 'Persian'
                    }, 
                    {
                        'name': 'Sphynx'
                    }
                ]
            }
        ]
    }

    linear_2 = [
        {'name': 'Pets', 'parent': None},
        {'name': 'Dogs', 'parent': 'Pets'},
        {'name': 'Poodle', 'parent': 'Dogs'},
        {'name': 'Dalmatian', 'parent': 'Dogs'},
        {'name': 'Husky', 'parent': 'Dogs'},
        {'name': 'Cats', 'parent': 'Pets'},
        {'name': 'Siamse', 'parent': 'Cats'},
        {'name': 'Persian', 'parent': 'Cats'},
        {'name': 'Sphynx', 'parent': 'Cats'}
    ]

    def test_hierarchical_to_linear_1(self):
        self.assertEqual(hierarchical_to_linear(
            hierarchical=self.hierarchical_1), self.linear_1)

    def test_linear_to_hierarchical_1(self):
        self.assertEqual(linear_to_hierarchical(
            linear=self.linear_1), self.hierarchical_1)

    def test_hierarchical_to_linear_2(self):
        self.assertEqual(hierarchical_to_linear(
            hierarchical=self.hierarchical__2), self.linear_2)

    def test_linear_to_hierarchical_2(self):
        self.assertEqual(linear_to_hierarchical(
            linear=self.linear_2), self.hierarchical__2)
