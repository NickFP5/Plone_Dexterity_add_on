
        # Integration tests for sessione_di_laurea
        ztc.ZopeDocFileSuite(
            'sessione_di_laurea.txt',
            package='lauree.tipi',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

