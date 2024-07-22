import os
import json


class HtmlPersistence:
    """ Save and retrieve data to and from storage """
    HTML_FOLDERNAME = "html_persistence"

    @staticmethod
    def store_evaluation_html(dct: dict[str:str], term: str) -> None:
        """Save dictionary as JSON file in location specified by file_name"""
        filename_prefix: str = f'{term}_evaluations'
        HtmlPersistence._save_json(dct, filename_prefix, HtmlPersistence.HTML_FOLDERNAME)

    @staticmethod
    def store_grade_html(dct: dict[str:str], term: str) -> None:
        """Save dictionary as JSON file in location specified by file_name"""
        filename_prefix: str = f'{term}_grades'
        HtmlPersistence._save_json(dct, filename_prefix, HtmlPersistence.HTML_FOLDERNAME)

    @staticmethod
    def store_information_html(dct: dict[str:str], term: str) -> None:
        """Save dictionary as JSON file in location specified by file_name"""
        filename_prefix: str = f'{term}_information'
        HtmlPersistence._save_json(dct, filename_prefix, HtmlPersistence.HTML_FOLDERNAME)

    @staticmethod
    def _save_json(dct: dict[str:str], filename_prefix: str, foldername: str) -> None:
        """Save dictionary as JSON file in location specified by file_name"""
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        file_location: str = f'{foldername}/{filename_prefix}.json'
        with open(file_location, mode='w', encoding="utf-8") as fp:
            json.dump(dct, fp)
            print('File has been saved: '+
                 f'{foldername}/{filename_prefix}.json')
