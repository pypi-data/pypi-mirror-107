# HTL - Library for transform data structures
## Example
```python
from htl.htl import linear_to_hierarchical, hierarchical_to_linear


linear = [
    {'name': 'Lorem',       'parent': None},
    {'name': 'ipsum',       'parent': 'Lorem'},
    {'name': 'dolor',       'parent': 'ipsum'},
    {'name': 'sit',         'parent': 'dolor'},
    {'name': 'amet',        'parent': 'ipsum'},
    {'name': 'consectetur', 'parent': 'Lorem'},
    {'name': 'adipisicing', 'parent': 'consectetur'}
]

hierarchical = linear_to_hierarchical(linear)

"""
hierarchical:
{
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
"""
# To reverse conversion, use function hierarchical_to_linear
```