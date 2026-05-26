"""Seed demo data: cities, stations, routes, buses, drivers, trips and a couple of news/FAQ entries."""
from datetime import datetime, timedelta
from decimal import Decimal
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import FAQ, HeroBanner, NewsArticle
from apps.routes.models import City, Route, RouteStop, Station
from apps.schedule.models import Bus, BusType, Driver, Trip

User = get_user_model()


CITIES = [
    ("Бишкек", "Чуйская область", "Кыргызстан"),
    ("Ош", "Ошская область", "Кыргызстан"),
    ("Каракол", "Иссык-Кульская область", "Кыргызстан"),
    ("Талас", "Таласская область", "Кыргызстан"),
    ("Нарын", "Нарынская область", "Кыргызстан"),
    ("Джалал-Абад", "Джалал-Абадская область", "Кыргызстан"),
    ("Балыкчы", "Иссык-Кульская область", "Кыргызстан"),
    ("Чолпон-Ата", "Иссык-Кульская область", "Кыргызстан"),
    ("Токмок", "Чуйская область", "Кыргызстан"),
    ("Кант", "Чуйская область", "Кыргызстан"),
    ("Алматы", "Алматинская область", "Казахстан"),
    ("Ташкент", "Ташкентская область", "Узбекистан"),
    ("Баткен", "Баткенская область", "Кыргызстан"),
    ("Кызыл-Кия", "Баткенская область", "Кыргызстан"),
    ("Кара-Суу", "Ошская область", "Кыргызстан"),
    ("Узген", "Ошская область", "Кыргызстан"),
    ("Араван", "Ошская область", "Кыргызстан"),
    ("Ноокат", "Ошская область", "Кыргызстан"),
]

STATIONS = {
    "Бишкек": [
        ("Западный автовокзал", "ул. Жибек-Жолу 299, Бишкек", "+996 312 654321"),
        ("Восточный автовокзал", "ул. Алматинская 1, Бишкек", "+996 312 123456"),
    ],
    "Ош": [("Главный автовокзал Ош", "ул. Заднепровского 9, Ош", "+996 3222 12345")],
    "Каракол": [("Автовокзал Каракол", "ул. Гагарина 173, Каракол", "+996 3922 54321")],
    "Талас": [("Автовокзал Талас", "ул. Бердике Баатыра 270, Талас", "+996 3422 11223")],
    "Нарын": [("Автовокзал Нарын", "ул. Ленина 88, Нарын", "+996 3522 33445")],
    "Джалал-Абад": [("Автовокзал Джалал-Абад", "ул. Ленина 14, Джалал-Абад", "+996 3722 66778")],
    "Балыкчы": [("Автовокзал Балыкчы", "ул. Береговая 2, Балыкчы", "+996 3944 11000")],
    "Чолпон-Ата": [("Автовокзал Чолпон-Ата", "ул. Советская 100, Чолпон-Ата", "+996 3943 22000")],
    "Токмок": [("Автовокзал Токмок", "ул. Ленина 220, Токмок", "+996 3138 11111")],
    "Кант": [("Автостанция Кант", "ул. Гагарина 5, Кант", "+996 3132 22222")],
    "Алматы": [("Сайран автовокзал", "пр. Толе би 296, Алматы", "+7 727 333 4444")],
    "Ташкент": [("Ташкентский автовокзал", "ул. Бунёдкор 18, Ташкент", "+998 71 555 6677")],
    "Баткен": [("Автовокзал Баткен", "ул. Салихова 12, Баткен", "+996 3622 12345")],
    "Кызыл-Кия": [("Автовокзал Кызыл-Кия", "ул. Первомайская 45, Кызыл-Кия", "+996 3657 54321")],
    "Кара-Суу": [("Автостанция Кара-Суу", "ул. Ленина 120, Кара-Суу", "+996 3232 11223")],
    "Узген": [("Автовокзал Узген", "ул. Манаса 54, Узген", "+996 3233 33445")],
    "Араван": [("Автостанция Араван", "ул. Космонавтов 12, Араван", "+996 3231 66778")],
    "Ноокат": [("Автостанция Ноокат", "ул. Федорова 9, Ноокат", "+996 3230 11000")],
}

# (origin_city, destination_city, distance_km, duration_min, base_price)
ROUTES = [
    ("Бишкек", "Ош", 615, 660, 1200),
    ("Бишкек", "Каракол", 400, 360, 700),
    ("Бишкек", "Талас", 310, 300, 600),
    ("Бишкек", "Нарын", 320, 300, 600),
    ("Бишкек", "Джалал-Абад", 580, 600, 1100),
    ("Бишкек", "Балыкчы", 170, 150, 350),
    ("Бишкек", "Чолпон-Ата", 270, 240, 500),
    ("Бишкек", "Токмок", 65, 60, 150),
    ("Бишкек", "Кант", 22, 30, 80),
    ("Бишкек", "Алматы", 240, 240, 800),
    ("Бишкек", "Ташкент", 580, 600, 1500),
    ("Ош", "Бишкек", 615, 660, 1200),
    ("Ош", "Джалал-Абад", 90, 90, 250),
    ("Ош", "Баткен", 240, 240, 500),
    ("Ош", "Кызыл-Кия", 85, 90, 200),
    ("Ош", "Кара-Суу", 25, 30, 60),
    ("Ош", "Узген", 55, 60, 150),
    ("Ош", "Араван", 35, 40, 100),
    ("Ош", "Ноокат", 45, 50, 120),
    ("Джалал-Абад", "Ош", 90, 90, 250),
    ("Каракол", "Чолпон-Ата", 130, 120, 250),
]

BUS_TYPES = [
    ("Минивэн Sprinter", "Комфортный минивэн на 18 мест", 18, False, True, False),
    ("Автобус Туристический", "Большой комфортабельный автобус", 45, True, True, True),
    ("Бус средний", "Средний автобус для региональных рейсов", 28, False, True, False),
]

BUSES = [
    ("01KG777AAA", "Mercedes Sprinter", 18, 5, 4, 0),  # bus_type_idx
    ("01KG888BBB", "Mercedes Sprinter", 18, 5, 4, 0),
    ("02KG111CCC", "Setra ComfortClass", 45, 12, 4, 1),
    ("03KG222DDD", "MAN Lion's Coach", 45, 12, 4, 1),
    ("01KG333EEE", "Higer KLQ6109", 28, 7, 4, 2),
    ("01KG444FFF", "Hyundai Universe", 28, 7, 4, 2),
]

DRIVERS = [
    ("Холматов Адылбек", "+996 700 111 111", "AB1234567", 12),
    ("Усенов Нурбек", "+996 700 222 222", "AB2345678", 8),
    ("Жумабаев Талант", "+996 700 333 333", "AB3456789", 15),
    ("Иманкулов Эрлан", "+996 700 444 444", "AB4567890", 6),
    ("Касымов Бакыт", "+996 700 555 555", "AB5678901", 20),
]


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными (города, автовокзалы, маршруты, рейсы)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=14, help="На сколько дней вперёд создавать рейсы")
        parser.add_argument("--clear", action="store_true", help="Очистить существующие данные перед сидированием")

    def handle(self, *args, **opts):
        if opts["clear"]:
            self.stdout.write(self.style.WARNING("Очищаем данные..."))
            Trip.objects.all().delete()
            Route.objects.all().delete()
            RouteStop.objects.all().delete()
            Station.objects.all().delete()
            City.objects.all().delete()
            Bus.objects.all().delete()
            BusType.objects.all().delete()
            Driver.objects.all().delete()

        self.stdout.write("Создаём города...")
        cities = {}
        for name, region, country in CITIES:
            c, _ = City.objects.get_or_create(name=name, defaults={"region": region, "country": country})
            cities[name] = c

        self.stdout.write("Создаём автовокзалы...")
        stations = {}
        for city_name, items in STATIONS.items():
            city = cities.get(city_name)
            if not city:
                continue
            for name, address, phone in items:
                s, _ = Station.objects.get_or_create(city=city, name=name, defaults={"address": address, "phone": phone})
                stations.setdefault(city_name, []).append(s)

        self.stdout.write("Создаём типы транспорта и автобусы...")
        bus_types = []
        for name, descr, seats, wifi, ac, toilet in BUS_TYPES:
            bt, _ = BusType.objects.get_or_create(
                name=name, defaults={"description": descr, "seats_default": seats, "has_wifi": wifi, "has_ac": ac, "has_toilet": toilet}
            )
            bus_types.append(bt)

        buses = []
        for plate, model, seats, rows, spr, bt_idx in BUSES:
            b, _ = Bus.objects.get_or_create(
                plate_number=plate,
                defaults={"model_name": model, "seats": seats, "rows": rows, "seats_per_row": spr, "bus_type": bus_types[bt_idx]},
            )
            buses.append(b)

        self.stdout.write("Создаём водителей...")
        drivers = []
        for name, phone, license_, exp in DRIVERS:
            d, _ = Driver.objects.get_or_create(
                full_name=name, defaults={"phone": phone, "license_number": license_, "experience_years": exp}
            )
            drivers.append(d)

        self.stdout.write("Создаём маршруты...")
        routes = []
        code_idx = 1
        for origin, dest, dist, dur, price in ROUTES:
            o_station = stations[origin][0]
            d_station = stations[dest][0]
            code = f"KG-{code_idx:03d}"
            r, _ = Route.objects.get_or_create(
                origin=o_station, destination=d_station,
                defaults={"code": code, "distance_km": dist, "duration_minutes": dur},
            )
            routes.append((r, Decimal(price)))
            code_idx += 1

        self.stdout.write("Создаём рейсы (оптимизированно)...")
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        trips_created = 0
        trips_to_create = []
        for day in range(opts["days"]):
            base_date = today + timedelta(days=day)
            for route, base_price in routes:
                # 2-4 рейса в день на маршрут
                num_trips = random.randint(2, 4)
                departure_hours = random.sample([6, 8, 10, 12, 14, 16, 18, 20, 22], num_trips)
                for hour in sorted(departure_hours):
                    departure = base_date.replace(hour=hour, minute=random.choice([0, 15, 30, 45]))
                    if departure < now:
                        continue
                    bus = random.choice(buses)
                    driver = random.choice(drivers)
                    # variance ±15%
                    price = base_price * Decimal(str(random.uniform(0.9, 1.15))).quantize(Decimal("0.01"))
                    trips_to_create.append(
                        Trip(
                            route=route, bus=bus, driver=driver,
                            departure_at=departure, base_price=price.quantize(Decimal("0.01")),
                        )
                    )
                    trips_created += 1

        Trip.objects.bulk_create(trips_to_create)

        self.stdout.write("Создаём контент (новости, FAQ, баннеры)...")
        NewsArticle.objects.get_or_create(
            slug="zapuskaem-platformu",
            defaults={
                "title": "Запускаем платформу AvtoBilet.kg!",
                "summary": "Теперь бронировать автобусные билеты можно онлайн за пару кликов.",
                "body": "Мы рады объявить о запуске единой платформы для онлайн-бронирования автобусных билетов в Кыргызстане. "
                        "Поддерживаются все основные направления, оплата картой и наличными в кассе.",
            },
        )
        NewsArticle.objects.get_or_create(
            slug="novyy-marshrut-bishkek-tashkent",
            defaults={
                "title": "Новый международный рейс Бишкек — Ташкент",
                "summary": "Ежедневные комфортабельные автобусы по выгодной цене.",
                "body": "С этой недели открыт регулярный рейс Бишкек — Ташкент. Wi-Fi, кондиционер, туалет на борту.",
            },
        )
        NewsArticle.objects.get_or_create(
            slug="detyam-skidka-50",
            defaults={
                "title": "Детям до 12 лет — скидка 50%",
                "summary": "Путешествуйте всей семьёй выгоднее.",
                "body": "Скидка действует при покупке любого рейса. Выберите чекбокс «Детский билет» при оформлении.",
            },
        )

        faqs = [
            ("Как купить билет?", "Выберите маршрут и дату на главной странице, выберите место и заполните данные пассажира — оплатите онлайн."),
            ("Можно ли вернуть билет?", "Да, до 2 часов до отправления — 90% стоимости, до 30 минут — 50%."),
            ("Нужно ли распечатывать билет?", "Нет. Просто покажите QR-код с телефона при посадке."),
            ("Какие способы оплаты доступны?", "Visa, MasterCard, Элкарт, MBank, O!Деньги, а также наличными в кассе автовокзала."),
            ("Что взять с собой?", "Документ, удостоверяющий личность (паспорт или ID-карту), и сам билет (электронный/распечатанный)."),
            ("Есть ли скидки?", "Дети до 12 лет — 50%. Студенты — 10% по промокоду STUDENT10."),
        ]
        for i, (q, a) in enumerate(faqs):
            FAQ.objects.get_or_create(question=q, defaults={"answer": a, "order": i})

        HeroBanner.objects.get_or_create(
            title="Билеты по всему Кыргызстану",
            defaults={
                "subtitle": "Online-бронирование с моментальным подтверждением",
                "cta_text": "Найти рейс",
                "cta_url": "/search/",
            },
        )

        # Create demo admin user if none
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser("admin", "admin@avtobilet.kg", "admin12345")
            self.stdout.write(self.style.SUCCESS("Создан admin / admin12345"))

        # Demo customer
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user("demo", "demo@avtobilet.kg", "demo12345", first_name="Айгуль", last_name="Демо", phone="+996 700 000 000")
            self.stdout.write(self.style.SUCCESS("Создан demo / demo12345"))

        self.stdout.write(self.style.SUCCESS(
            f"Готово! Городов: {len(cities)}, маршрутов: {len(routes)}, рейсов создано: {trips_created}."
        ))
