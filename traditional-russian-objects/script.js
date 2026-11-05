// Пункты меню: [папка, название]
const folders = [
  ["chugunok", "Чугунок"],
  ["hlebnaya-lopata", "Хлебная лопата"],
  ["kadka", "Кадка"],
  ["kerosinovaya-lampa", "Керосиновая лампа"],
  ["koromyslo", "Коромысло"],
  ["koryto", "Корыто"],
  ["korzina", "Корзина"],
  ["krasnyi-ugol", "Красный угол"],
  ["krynka", "Крынка"],
  ["kukly", "Куклы"],
  ["len", "Лён"],
  ["letnyaya-krestyanskaya-obuv", "Летняя крестьянская обувь"],
  ["lyulka", "Люлька"],
  ["myalitsa", "Мялица"],
  ["rubel", "Рубель"],
  ["ruchnye-pryalki", "Ручные прялки"],
  ["russkaya-pech", "Русская печь"],
  ["samopryalki", "Самопрялки"],
  ["samovar", "Самовар"],
  ["tatahtushka", "Татахтушка"],
  ["tkatskii-stanok", "Ткацкий станок"],
  ["uhvat", "Ухват"],
  ["utyug", "Утюг"],
  ["valenki", "Валенки"],
  ["zimnyaya-krestyanskaya-obuv", "Зимняя крестьянская обувь"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
