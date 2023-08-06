class Group:
  """
    Builds a group using an identifier and storing values with that identifier.

    Remember that having your values as a set doesn't support item assignment.

    ...

    Attributes
    ----------
    name : str
        The string identifier of the group
    identifier : str
        An alias for `name`.
    values : Any
        Can be a list, dict, set, or any 
        other type that represents the 
        pygroups' values.
    content : Any
        An alias for `values`.

    Methods
    -------
    set_name(name=None)
        Sets the name of the group instance. 
        Will throw an error if no name is 
        specified (can't have a nameless 
        group! :|)
    """
  def __init__(self, identifier : str = None, content : list = None):
    if identifier == None:
      raise ValueError("Cannot instantiate a group without a title.")
    if content == None:
      raise ValueError("Cannot instantiate a group without content.")
    self.name = identifier
    self.identifier = identifier
    self.values = content
    self.content = content 
    self.index = len(self.content)

  def set_name(self, name=None):
    """
      Sets the name of the group instance. 
      Will throw an error if no name is 
      specified (can't have a nameless 
      group! :|)
    """
    if name is None:
      raise ValueError("Name of a group can't be None.")
    else:
      self.name = name

  def __iter__(self):
    return self

  def __next__(self):
    if self.index == 0:
      raise StopIteration
    self.index = self.index - 1
    return self.values[self.index]
    

    