// Пункты меню: [папка, название]
const folders = [
  ["arka-vdnh", "Арка ВДНХ"],
  ["bolshoy-teatr", "Большой театр"],
  ["cirk-na-cvetnom-bulvare", "Цирк на Цветном бульваре"],
  ["izmailovskiy-kreml", "Измайловский Кремль"],
  ["khram-vasiliya-blazhennogo", "Храм Василия Блаженного"],
  ["moskovskiy-gosudarstvennyy-universitet", "МГУ"],
  ["moskovskiy-metropoliten", "Московский метрополитен"],
  ["moskovskiy-zoopark", "Московский зоопарк"],
  ["moskva-siti", "Москва-Сити"],
  ["ostankinskaya-bashnya", "Останкинская башня"],
  ["park-sokolniki", "Парк Сокольники"],
  ["rostokinskiy-akveduk-gidrotehnicheskoe-sooruzhenie", "Ростокинский акведук. Гидротехническое сооружение"],
  ["severnyy-rechnoy-vokzal", "Северный речной вокзал"],
  ["spasskaya-bashnya-kremla", "Спасская башня Кремля"],
  ["teatr-kukol", "Театр кукол"],
  ["triumfalnaya-arka", "Триумфальная арка"],
  ["vdnh-aviaciya-i-kosmos", "ВДНХ. Авиация и космос"],
  ["vdnh-gorodskaya-ferma", "ВДНХ. Городская ферма"],
  ["vdnh-robostanciya", "ВДНХ. Робостанция"],
  ["zhivopisnyy-most", "Живописный мост"],
  ["zhivoy-mir-kuzminkok-domik-dlya-ptic", "Живой мир кузьминок. Домик для птиц"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
