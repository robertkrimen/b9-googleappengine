from b9 import parse

def test():
    parser = parse.Parser(source = {
        'none': None,
        'empty': ''
    })
    assert None == parser.get('none')
    assert '' == parser.get('empty')
    assert None == parser.get('none', 1)
    assert 1 == parser.get('none', none = 1)

    parser = parse.Parser(map = """
    Apple apple
    Banana banana
    """
    )
    assert 'apple' == parser._map['Apple']
    assert 'banana' == parser._map['Banana']

#    parser.error('Blech! Yoink!')
#    parser.check()
