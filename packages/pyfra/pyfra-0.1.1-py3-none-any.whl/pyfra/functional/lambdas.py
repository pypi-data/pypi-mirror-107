

__all__ = ['X', 'Y']


Y = object()


class Reflective:
    def __init__(self, stack):
        self.stack = stack

    def __getattr__(self, a):
        return Reflective(self.stack + [('attr', a)])#_fn
    
    def __getitem__(self, a):
        return Reflective(self.stack + [('arr', a)]) #lambda x: x[a]
    
    def __mul__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return x * y
            return  _f
        
        return lambda x: x * other
    
    def __rmul__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return y * x
            return  _f
        
        return lambda x: other * x
    
    def __add__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return x + y
            return  _f
        
        return lambda x: x + other
    
    def __radd__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return y + x
            return  _f
        
        return lambda x: other + x
    
    def __gt__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return x > y
            return  _f
        
        return lambda x: x > other
    
    def __lt__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return x < y
            return  _f
        
        return lambda x: x < other
    
    def __rgt__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return y > x
            return  _f
        
        return lambda x: other > x
    
    def __rlt__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return y < x
            return  _f
        
        return lambda x: other < x
    
    def __eq__(self, other):
        if other == Y:
            def _f(x, y=None):
                if y == None:
                    x, y = x
                
                return x == y
            return  _f
        
        return lambda x: x == other
    
    def __call__(self, *args, **kwargs):
        return Reflective(self.stack + [('call', (args, kwargs))]) #lambda x: x[a]
    
    def run(self, x):
        for t, f in self.stack:
            if t == 'attr':
                x = getattr(x, f)
            elif t == 'call':
                args, kwargs = f
                x = x(*args, **kwargs)
            else:
                x = x[f]

        return x



X = Reflective([])