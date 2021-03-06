import unittest
import os

from pymlstats.main import MailingList, COMPRESSED_DIR


class MailingListTest(unittest.TestCase):
    def check_single_dict(self, expected, result):
        for key, value in expected.items():
            output = u"{}:\n" \
                     u"\tExpected: '{}'\n" \
                     u"\tObtained: '{}'".format(key, value, result[key])
            self.assertEqual(value, result[key], output)

    def test_mailing_list_0(self):
        '''Remote URL with no trailing slash'''
        ml = MailingList('http://mlstats.org/pipermail/mlstats-list')
        target = 'mlstats.org/pipermail/mlstats-list'
        expected = {
            'location': 'http://mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': False,
            'is_remote': True,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_1(self):
        '''Remote URL with trailing slash'''
        ml = MailingList('http://mlstats.org/pipermail/mlstats-list/')
        target = 'mlstats.org/pipermail/mlstats-list'
        expected = {
            'location': 'http://mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': False,
            'is_remote': True,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_2(self):
        '''Remote short URL with no trailing slash'''
        ml = MailingList('http://mlstats.org')
        target = 'mlstats.org'
        expected = {
            'location': 'http://mlstats.org',
            'alias': 'mlstats.org',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': False,
            'is_remote': True,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_3(self):
        '''Remote short URL with trailing slash'''
        ml = MailingList('http://mlstats.org/')
        target = 'mlstats.org'
        expected = {
            'location': 'http://mlstats.org',
            'alias': 'mlstats.org',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': False,
            'is_remote': True,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_4(self):
        '''Local directory with no trailing slash'''
        ml = MailingList('/mlstats.org/pipermail/mlstats-list')
        target = 'mlstats.org/pipermail/mlstats-list'
        expected = {
            'location': '/mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_5(self):
        '''Local directory with trailing slash'''
        ml = MailingList('/mlstats.org/pipermail/mlstats-list/')
        target = 'mlstats.org/pipermail/mlstats-list'
        expected = {
            'location': '/mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_6(self):
        '''Local directory in .mlstats with no trailing slash'''
        base = os.path.sep.join([COMPRESSED_DIR,
                                'mlstats.org/pipermail/mlstats-list'])
        target = base.lstrip(os.path.sep)
        ml = MailingList(base)
        expected = {
            'location': base.rstrip(os.path.sep),
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_7(self):
        '''Local directory in .mlstats with trailing slash'''
        base = os.path.sep.join([COMPRESSED_DIR,
                                'mlstats.org/pipermail/mlstats-list/'])
        ml = MailingList(base)
        target = base.strip(os.path.sep)
        expected = {
            'location': base.rstrip(os.path.sep),
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_8(self):
        '''Local URL (file://) with no trailing slash'''
        base = 'file:///mlstats.org/pipermail/mlstats-list'
        target = '/mlstats.org/pipermail/mlstats-list'.lstrip(os.path.sep)
        ml = MailingList(base)
        expected = {
            'location': '/mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)

    def test_mailing_list_9(self):
        '''Local URL (file://) with trailing slash'''
        base = 'file:///mlstats.org/pipermail/mlstats-list/'
        ml = MailingList(base)
        target = '/mlstats.org/pipermail/mlstats-list'.lstrip(os.path.sep)
        expected = {
            'location': '/mlstats.org/pipermail/mlstats-list',
            'alias': 'mlstats-list',
            'compressed_dir': os.path.join(COMPRESSED_DIR, target),
            'is_local': True,
            'is_remote': False,
        }

        result = {
            'location': ml.location,
            'alias': ml.alias,
            'compressed_dir': ml.compressed_dir,
            'is_local': ml.is_local(),
            'is_remote': ml.is_remote(),
        }
        self.check_single_dict(expected, result)
