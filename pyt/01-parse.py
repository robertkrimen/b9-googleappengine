from b9 import parse

def test():
    parser = parse.Parser(source = {
        'none': None,
        'empty': ''
    })
    assert None == parser.get( 'none' )
    assert '' == parser.get( 'empty' )
    assert 1 == parser.get( 'none', none = 1 )

    assert parser.empty( 'empty' )
    assert parser.none( 'none' )

    assert 1 == parser.load( 'none', none = 1 )
    assert 1 == parser.get( 'none' )

    parser = parse.Parser(map = """
        apple Apple
        banana Banana
        cherry % %_
    """
    )
    assert ('Apple', ) == parser._map[ 'apple' ]
    assert ('Banana', ) == parser._map[ 'banana' ]
    assert ('cherry', 'cherry_', ) == parser._map[ 'cherry' ]

    parser.set({ 'one': 1, 'two': 2 })
    assert 1 == parser.get( 'one' )
    assert 2 == parser.get( 'two' )
    parser.set('three', 3)
    assert 3 == parser.get( 'three' )

    slice = parser.slice("one two three".split())
    assert 1 == slice[ 'one' ]
    assert 2 == slice[ 'two' ]
    assert 3 == slice[ 'three' ]
    assert 'apple' not in slice
    assert 'banana' not in slice

    assert int == type( parser.get( 'one', ) )
    assert str == type( parser.get( 'one', into = str ) )

    assert int == type( parser.load( 'one', ) )
    assert str == type( parser.get( 'one', into = str ) )
    assert str == type( parser.load( 'one', into = str ) )
    assert str == type( parser.get( 'one', ) )
    assert str == type( parser.load( 'one', ) )
    assert int == type( parser.load( 'one', into = int ) )
    assert int == type( parser.get( 'one', ) )

    parser = parse.Parser(map = """
        canonical primary secondary
    """, source = {
        'primary': 'good',
        'secondary': 'bad',
    })
    assert 'good' == parser.get( 'canonical' )

    parser = parse.Parser(map = """
        primary secondary primary
    """, source = {
        'primary': 'bad',
        'secondary': 'good',
    })
    assert 'good' == parser.get( 'primary' )
#    assert int == type( parser.get( 'one' ) )

#    parser.error('Blech! Yoink!')
#    parser.check()
