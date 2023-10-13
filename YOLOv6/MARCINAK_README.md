Ez az a repo amit ide feltettem és akkor ez alapján lehet fine-tune olni az egyik már kész modelt: https://github.com/meituan/YOLOv6/blob/main/docs/Train_custom_data.md

Bár félek hogy ilyen kényelmesen nem fog menni, eddig nem is tanult rendszámokra hanem egy csomó minden másra. Akkor lehet meg kell próbálni from scratch tanítani csak a mi képeink alapján. Minden elő van készítve hogy a yolo-v6-s6-ot finomhangolhasd, max a weights fájlt nem engedi majd a github (configs/weights). 

A custom databan ottvannak 3 mappába szervezve a képek meg a labelek. A remover.py végigmegy a test/train/val mappákon, megnézi hogy milyen labelek vannak bennük, és azokat a képeket kitörli amiknek nincs labelje.