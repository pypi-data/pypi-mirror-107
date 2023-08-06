import unittest
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.platform_data_aggregator.ext_services.yandex_maps.parser.parsing_yandex_maps import parser_yandex
from services_reviews.platform_data_aggregator.ext_services.yandex_maps.parser.mocks.parser_result_mock import parser_res_mock
from services_reviews.common_configs import DB_CONFIG_DIR, EXT_PLATFORM_CONFIG_DIR

class parsing_yandex_test(unittest.TestCase):
    def test_1(self):
        ReadConf.read("ES", EXT_PLATFORM_CONFIG_DIR)
        ReadConf.read("db", DB_CONFIG_DIR)

        self.maxDiff = None
        businessId = 1028036697
        page = 1
        json = parser_yandex(businessId,page,pageSize=5)[0].get('data', None)
        self.assertTrue('reviews' in json)


