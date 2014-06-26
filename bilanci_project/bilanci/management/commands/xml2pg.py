from collections import OrderedDict
import logging
from optparse import make_option
from django.conf import settings
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from bilanci.utils.comuni import FLMapper
from territori.models import Territorio, ObjectDoesNotExist


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
                    dest='dryrun',
                    action='store_true',
                    default=False,
                    help='Set the dry-run command mode: nothing is written on the db'),

        make_option('--file',
                    dest='input_file',
                    default='',
                    help='Input Xml file to parse'),
        make_option('--append',
                    dest='append',
                    action='store_true',
                    default=False,
                    help='Use the log file appending instead of overwriting (used when launching shell scripts)'),
    )

    help = 'Import xml bilancio files into pg db'

    logger = logging.getLogger('management')
    comuni_dicts = {}


    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity == '0':
            self.logger.setLevel(logging.ERROR)
        elif verbosity == '1':
            self.logger.setLevel(logging.WARNING)
        elif verbosity == '2':
            self.logger.setLevel(logging.INFO)
        elif verbosity == '3':
            self.logger.setLevel(logging.DEBUG)

        dryrun = options['dryrun']
        input_file = options['input_file']

        if options['append'] is True:
            self.logger = logging.getLogger('management_append')

        # open input file
        soup = BeautifulSoup(open(input_file),"xml")
        x = True

        # get finloc, year, tipo bilancio
        certificato = soup.certificato
        codiceEnte = certificato['codiceEnte']
        anno = certificato['anno']
        tipoCertificato = certificato['tipoCertificato']

        # get all elements
        colonne_set = soup.find_all('colonne')
        for colonne in colonne_set:
            print "Quadro:{0} voce:{1}".format(colonne['quadro'], colonne['voce'])

            for colonna in colonne.contents:
                if colonna != u'\n':
                    print "colonna n:{0} value:{1}".format(colonna['num'], colonna.string)