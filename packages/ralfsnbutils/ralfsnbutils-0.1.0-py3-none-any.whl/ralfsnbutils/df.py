def cpshow(self, n=5, name=None, cache=True):
    """Count dataframe's rows and show it's n first rows in a pandas dataframe"""
    if name is None:
        name = "DataFrame"
    if cache:
        self = self.cache()
    print(f"{name} has {self.count()} rows")
    return self.limit(n).toPandas()
