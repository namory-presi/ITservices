from .basket import Basket


def basket(request):
    baskets = Basket(request=request)
    return dict(baskets=baskets)