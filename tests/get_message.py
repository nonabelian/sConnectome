# Simple message format for test assertion:

def get_message(name, expected, actual):
    ''' Formats assertion message
        INPUT: string, code, code
        OUTPUT: string
    '''
    message = '{0} was {2} instead of {1}'
    return message.format(name, expected, actual)
