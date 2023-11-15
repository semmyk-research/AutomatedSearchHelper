from TextSearchEngine.search_functions import *

# finder = AND(
#     PARTIAL_WORD("mutation testing"),
#     OR(
#         EXACT_WORD("C", caseSensitive = True),
#         EXACT_WORD("LLVM", caseSensitive = True)))

'''
finder = AND(
    PARTIAL_WORD("mutation testing"))
'''
    
## AKA_Feb22
finder = AND(
        EXACT_WORD("digital technology", caseSensitive = False),
        OR(
            EXACT_WORD("digital technologies", caseSensitive = False)),
            AND(
                PARTIAL_WORD("define"),
                AND(
                EXACT_WORD("digital transformation", caseSensitive = False)
                )))
        
        '''
        AND(EXACT_WORD("digital technology", caseSensitive = False), OR(EXACT_WORD("digital technologies", caseSensitive = False)), AND(PARTIAL_WORD("define"), AND(EXACT_WORD("digital transformation", caseSensitive = False))))
        '''
        
        '''
        finder = AND(
    PARTIAL_WORD("define"),
    AND(
        EXACT_WORD("digital technology", caseSensitive = False),
        OR(EXACT_WORD("digital technologies", caseSensitive = False))
        ))
        '''