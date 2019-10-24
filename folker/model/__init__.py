

#
# class TestData:
#     name: str
#     description: str
#     stages: [StageData]
#
#     def __init__(self,
#                  test_name='UNDEFINED',
#                  test_description='None',
#                  stages: [StageData] = None) -> None:
#         super().__init__()
#         self.name = test_name
#         self.description = test_description
#         self.stages = stages
from folker.model.data import StageData


class Stage:
    data: StageData

