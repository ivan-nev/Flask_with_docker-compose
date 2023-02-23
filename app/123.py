from server import get_advertisement
from db import Session

with Session() as session:
    adv = get_advertisement(1,session)
    print(adv.title)
    print(adv.advertisements.username)

