import ast
from collections import OrderedDict
from typing import TypeVar, Type, List, Tuple

from requests import Response
from box import Box
from box.exceptions import BoxKeyError

from confluence.cli import utils

T = TypeVar('T')


## [space, user, page, blogpost, comment, attachment]


class Foo:
    """Helping class to extract and compare static an class method types using:
    type(__dict__.get(method))"""

    @staticmethod
    def foo_static():
        pass

    @classmethod
    def foo_class(cls):
        pass


StaticMethodType = type(Foo.__dict__.get("foo_static"))
ClassMethodType = type(Foo.__dict__.get("foo_class"))


class NavigableDict(Box):    
    @classmethod
    def from_response(cls: Type[T], response: Response) -> T:
        obj = cls.__new__(cls)
        obj.__init__(response.json(), default_box=True, default_box_attr=None, box_dots=True)
        return obj

    @classmethod
    def from_results(cls: Type[T], results: dict) -> List[T]:
        lst: List[T] = list()
        for result in results:
            obj = cls.__new__(cls)
            obj.__init__(result, default_box=True, default_box_attr=None, box_dots=True)
            lst.append(obj)
        return lst


class Page(NavigableDict):
    """Data class for containing Confluence Page responses with some property utilities for
    .id .version .title ..."""

    ## Explicit properties
    #@property
    #def id(self):
    #    return self.id
    #@property
    #def type(self):
    #    return self.type

    @property
    def version(self):
        return self.version.number

    #@property
    #def title(self):
    #    return self.title

    @property
    def body_storage(self):
        return self.body.storage.value

    @property
    def body_view(self):
        return self.body.export_view.value

    @property
    def parent(self):
        if self.ancestors:
            return utils.type_wrap(self.ancestors[-1])
        else:
            return None


class BlogPost(Page):
    pass


class Comment(Page):
    pass


class Space(NavigableDict):

    @property
    def desc(self):        
        return self.description.plain.value

    @property
    def labels(self):
        return [result["name"] for result in self.metadata.labels.results]


class User(NavigableDict):
    pass


JSONResponses = List[NavigableDict]
Pages = List[Page]
BlogPosts = List[BlogPost]
Comments = List[Comment]
Spaces = List[Space]
Users = List[User]


# class NavigableDict2(OrderedDict):
#     """ Allows jst.get(str) jst[int] and jst['var1.var2.var3'] or
#     jst.get('var1.var2.var3')"""
# 
#     def __setitem__(self, key, myvalue):
#         super().__setitem__(key, myvalue)
#         self.move_to_end(key)
# 
#     def __getitem__(self, key=None):
#         if type(key) == int:
#             myvalue = list(self.items())[key][1]
#         elif type(key) == slice:
#             myvalue = list(self.items())[key]
#         else:
#             myvalue = self.get(key, restval=None)
#             if myvalue is None:
#                 raise KeyError(key)
#         return myvalue
# 
#     # __getattr__ = __getitem__
#     def __getattr__(self, attr):
#         ## Implicit property
#         value = super().get(attr)
#         return NavigableDict(value) if type(value) == dict else value
# 
#     def get(self, key, restval=None):
#         value = super().get(key)
#         if type(key) == str and str(key).rfind(".") != -1:
#             value = self.get_value_for_composed_key(key, restval)
#         elif value is None:
#             value = restval
#         return value
# 
#     def get_item_as_dict(self, key) -> dict:
#         if isinstance(self.get(key), dict):
#             return dict(self.get(key, {}).items())
#         else:
#             try:
#                 return ast.literal_eval(str(self.get(key)))
#             except ValueError:
#                 raise ValueError(f"ast Error '{key}' value can't be evaluated as dict")
# 
#     def get_value_for_composed_key(self, key, restval=None):
#         keys = str(key).split(".")
#         value = self
#         for key in keys:
#             value = value.get(key)
#         return value
# 
#     @classmethod
#     def from_response(cls: Type[T], response: Response) -> T:
#         obj = cls.__new__(cls)
#         obj.__init__(response.json())
#         return obj
# 
#     @classmethod
#     def from_results(cls: Type[T], results: dict) -> List[T]:
#         lst: List[T] = list()
#         for result in results:
#             obj = cls.__new__(cls)
#             obj.__init__(result)
#             lst.append(obj)
#         return lst
# 