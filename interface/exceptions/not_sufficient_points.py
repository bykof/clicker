class NotSufficientPoints(Exception):
    def __str__(self):
        return f'No sufficient points for operation'
