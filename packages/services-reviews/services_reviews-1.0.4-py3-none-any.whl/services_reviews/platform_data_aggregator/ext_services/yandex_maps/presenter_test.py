import unittest
from services_reviews.platform_data_aggregator.ext_services.yandex_maps.presenter import loop_page_parsing

class presenter_yandex_test(unittest.TestCase):
    def test_1(self):
        self.maxDiff = None
        businessId = 1028036697
        page = 1
        # print(parser_yandex(businessId,54,pageSize=10))
        # self.assertEqual(parser_yandex(businessId,page,pageSize=1),(parser_res_mock,743))

    def test_2(self):
        businessId = 1028036697
        # print(loop_page_parsing(businessId))