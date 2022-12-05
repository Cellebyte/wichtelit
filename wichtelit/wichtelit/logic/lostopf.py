import random
import logging
import secrets
from typing import List

from ..models import Status, Wichtelmember

logger = logging.getLogger(__name__)


class LosTopf(object):

    @staticmethod
    def scrambled(original):
        dest = original[:]
        random.shuffle(dest)
        return dest

    def ziehen(members: List[Wichtelmember], lostopf: List[Wichtelmember]):
        for index in range(len(members)):
            lostopf = LosTopf.scrambled(lostopf)
            not_in_list = False
            loszieher = members[index]
            try:
                lostopf.remove(loszieher)
            except ValueError:
                not_in_list = True
            loszieher.wichtelpartner = secrets.choice(
                lostopf
            )
            logger.debug(
                f'{loszieher.emailAdresse} --> {loszieher.wichtelpartner.emailAdresse}')
            loszieher.status = Status.GEWÜRFELT
            loszieher.save()
            lostopf.remove(loszieher.wichtelpartner)
            if not not_in_list:
                lostopf.append(loszieher)
