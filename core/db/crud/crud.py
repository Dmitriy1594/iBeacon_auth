"""
crud.py

created by dromakin as 17.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__copyright__ = "Cybertonica LLC, London, 2020"
__status__ = 'Development'
__version__ = '20201117'

from typing import List, Optional, Dict

from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.db import models
from core.db.schemes import beacons as schemas

from core.db.crud.crud_pis import get_pi_by_name

from core.auth.token import api_token_hash, generate_random_token


# Multi method
def get_count_visitors_by_name(
    db: Session,
    name: str,
):
    lots = db.query(models.Beacon).filter(
        models.Beacon.product_name == name,
    ).count()

    db.query(models.Raspberry).filter(
        models.Raspberry.name == name,
    ).update(
        {
            "count_visitors": int(lots),
        }
    )
    db.commit()
    db_pi = get_pi_by_name(db, name)
    return db_pi
