// Массив папок: [имя папки на диске, отображаемое имя на русском]
const folders = [
  ["zhivopisnyy-most", "Живописный мост"],
  ["izmailovskiy-kreml", "Измайловский Кремль"],
  ["moskovskiy-gosudarstvennyy-universitet", "МГУ"],
  ["moskovskiy-metropoliten", "Московский метрополитен"],
  ["ostankinskaya-bashnya", "Останкинская башня"],
  ["severnyy-rechnoy-vokzal", "Северный речной вокзал"],
  ["spasskaya-bashnya-kremla", "Спасская башня Кремля"],
  ["khram-vasiliya-blazhennogo", "Храм Василия Блаженного"],

  // ——— Дополнения ———
  ["arka-vdnh", "Арка ВДНХ"],
  ["bolshoy-teatr", "Большой театр"],
  ["vdnh-aviaciya-i-kosmos", "ВДНХ. Авиация и космос"],
  ["vdnh-gorodskaya-ferma", "ВДНХ. Городская ферма"],
  ["vdnh-robostanciya", "ВДНХ. Робостанция"],
  ["zhivoy-mir-kuzminkok-domik-dlya-ptic", "Живой мир кузьминок. Домик для птиц"],
  ["moskva-siti", "Москва-Сити"],
  ["moskovskiy-zoopark", "Московский зоопарк"],
  ["park-sokolniki", "Парк Сокольники"],
  ["rostokinskiy-akveduk-gidrotehnicheskoe-sooruzhenie", "Ростокинский акведук. Гидротехническое сооружение"],
  ["teatr-kukol", "Театр кукол"],
  ["triumfalnaya-arka", "Триумфальная арка"],
  ["cirk-na-cvetnom-bulvare", "Цирк на Цветном бульваре"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;  // путь совпадает с именем папки
  link.className = "item";
  link.textContent = displayName;      // отображаем красивое имя
  menu.appendChild(link);
});