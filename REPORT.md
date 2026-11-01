# Статический анализ и детекция SDK в Android-приложениях из RuStore

## 1. Сводная статистика

Исследованы **10 APK** по базе из **25 SDK**. Обнаружены компоненты **21 SDK**, всего **80 пар «приложение — SDK»**.

- **Аналитика:** AppMetrica — в 9 приложениях, Firebase Analytics — в 4, MyTracker — в 3.
- **Push-уведомления:** Firebase Cloud Messaging — в 10, AppMetrica Push — в 5, Huawei Push — в 4, RuStore Push — в 3.
- **Платежные системы:** RuStore Billing и T-Bank Acquiring не обнаружены.
- **Картография:** Yandex MapKit — в 1 приложении; 2GIS SDK не обнаружен.

## 2. Анализ импортозамещения

На отечественные решения приходится **41,25%** найденных пар «приложение — SDK», на зарубежные — **58,75%**.

1. **Push-сервисы:** во всех трёх приложениях с RuStore Push также присутствует FCM.
2. **Аналитика:** AppMetrica встречается чаще Firebase Analytics, но в четырёх приложениях они присутствуют совместно.
3. **Авторизация:** компоненты Google Sign-In найдены в 10 приложениях, Yandex Login — в 2; VK ID не обнаружен.

Результаты показывают совместное присутствие отечественных и зарубежных компонентов, а не полную замену. Выводы относятся только к исследованным APK.

## 3. Сложности статического анализа

- **Обфускация:** переименование классов затрудняет поиск; использовались признаки из DEX, манифеста и нативных библиотек.
- **Динамическая загрузка:** код, загружаемый после установки, и отсутствующие split-APK не учитывались.
- **Ограничения обнаружения:** наличие компонентов SDK не подтверждает использование его функций. Отсутствие известных платежных SDK не означает отсутствия оплаты в приложении.

## 4. Источники

Инструменты. 

- Rustore downloader: https://github.com/k7361/rustore-downloader
- JADX: https://github.com/skylot/jadx

Ссылки для всех 25 SDK приведены в `sdk_database.json`.

- RuStore Push SDK: https://nexus-external.rustore.ru/repository/maven-rustore-exposed/
- RuStore BillingClient SDK (legacy): https://nexus-external.rustore.ru/repository/maven-rustore-exposed/
- Yandex AppMetrica: https://github.com/appmetrica/appmetrica-sdk-android
- Yandex MapKit SDK: https://repo.maven.apache.org/maven2/com/yandex/android/maps.mobile/
- Yandex Mobile Ads SDK: https://repo.maven.apache.org/maven2
- VK ID SDK: https://github.com/VKCOM/vkid-android-sdk
- MyTracker Analytics: https://github.com/myTrackerSDK/mytracker-android
- T-Bank Acquiring SDK: https://github.com/tinkoff-mobile-tech/tinkoff-asdk-android
- 2GIS Map SDK: https://artifactory.2gis.dev/sdk-maven-release/
- Huawei HMS Push SDK: https://developer.huawei.com/repo
- Firebase Cloud Messaging: https://maven.google.com
- Google Analytics for Firebase: https://maven.google.com
- Sentry Android Crash Reporting: https://github.com/getsentry/sentry-java
- Firebase Crashlytics: https://github.com/firebase/firebase-android-sdk
- myTarget SDK: https://github.com/myTargetSDK/mytarget-android
- AppMetrica Push SDK: https://github.com/appmetrica/push-sdk-android
- AppsFlyer Android SDK: https://repo.maven.apache.org/maven2/com/appsflyer/af-android-sdk/
- Yandex Login SDK: https://github.com/yandexmobile/yandex-login-sdk-android
- Google Sign-In (Google Play services Auth): https://dl.google.com/dl/android/maven2/com/google/android/gms/play-services-auth/
- Firebase Performance Monitoring: https://github.com/firebase/firebase-android-sdk/tree/master/firebase-perf
- Firebase Remote Config: https://github.com/firebase/firebase-android-sdk/tree/master/firebase-config
- Firebase Dynamic Links (legacy): https://dl.google.com/dl/android/maven2/com/google/firebase/firebase-dynamic-links/
- Google ML Kit Barcode Scanning: https://dl.google.com/dl/android/maven2/com/google/mlkit/barcode-scanning/
- Huawei HMS Location Kit: https://developer.huawei.com/repo/com/huawei/hms/location/
- Yandex DivKit Android: https://github.com/divkit/divkit

Ссылки для всех 10 APK приведены.

- Яндекс Календарь: https://www.rustore.ru/catalog/app/com.yandex.calendar.app
- Кинопоиск: кино и сериалы: https://www.rustore.ru/catalog/app/ru.kinopoisk
- МАКС: общение, звонки, сервисы: https://www.rustore.ru/catalog/app/ru.oneme.app
- Яндекс Книги: https://www.rustore.ru/catalog/app/ru.plus.bookmate
- Пятёрочка: доставка продуктов: https://www.rustore.ru/catalog/app/ru.pyaterochka.app.browser
- RUTUBE: видео, шоу, трансляции: https://www.rustore.ru/catalog/app/ru.rutube.app
- Яндекс Музыка, книги, подкасты: https://www.rustore.ru/catalog/app/ru.yandex.music
- Яндекс Переводчик: https://www.rustore.ru/catalog/app/ru.yandex.translate
- Яндекс Погода — Карта осадков: https://www.rustore.ru/catalog/app/ru.yandex.weatherplugin
- Дзен: https://www.rustore.ru/catalog/app/ru.zen.android
