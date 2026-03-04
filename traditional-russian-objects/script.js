// Массив папок: [имя папки на диске, отображаемое имя на русском]
const folders = [
  ["valenki", "Валенки"],
  ["zimnyaya-krestyanskaya-obuv", "Зимняя крестьянская обувь"],
  ["kadka", "Кадка"],
  ["kerosinovaya-lampa", "Керосиновая лампа"],
  ["korzina", "Корзина"],
  ["koromyslo", "Коромысло"],
  ["koryto", "Корыто"],
  ["krasnyi-ugol", "Красный угол"],
  ["krynka", "Крынка"],
  ["kukly", "Куклы"],
  ["len", "Лён"],
  ["letnyaya-krestyanskaya-obuv", "Летняя крестьянская обувь"],
  ["lyulka", "Люлька"],
  ["myalitsa", "Мялица"],
  ["rubel", "Рубель"],
  ["russkaya-pech", "Русская печь"],
  ["ruchnye-pryalki", "Ручные прялки"],
  ["samopryalki", "Самопрялки"],
  ["samovar", "Самовар"],
  ["tatahtushka", "Татахтушка"],
  ["tkatskii-stanok", "Ткацкий станок"],
  ["utyug", "Утюг"],
  ["uhvat", "Ухват"],
  ["hlebnaya-lopata", "Хлебная лопата"],
  ["chugunok", "Чугунок"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;  // путь совпадает с именем папки
  link.className = "item";
  link.textContent = displayName;      // отображаем красивое имя
  menu.appendChild(link);
});