import logging
import secrets
from typing import List

from ..models import Wichtelmember

logger = logging.getLogger(__name__)


class LosTopf(object):

    @staticmethod
    def ziehen(members: List[Wichtelmember], lostopf: List[Wichtelmember]):
        for index in range(len(members)):
            not_in_list = False
            loszieher = members[index]
            try:
                lostopf.remove(loszieher.id)
            except ValueError:
                not_in_list = True
            loszieher.wichtelpartner = secrets.choice(
                lostopf
            )
            logger.info(
                f'{loszieher.emailAdresse} hat partner {loszieher.wichtelpartner.emailAdresse}')
            loszieher.save()
            lostopf.remove(loszieher.wichtelpartner)
            if not not_in_list:
                lostopf.append(loszieher)
