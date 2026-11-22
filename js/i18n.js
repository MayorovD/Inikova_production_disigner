/* Client-side language switch: default Russian, English on toggle.
   Default language stays Russian; English is applied instantly and remembered in localStorage. */
(function () {
  "use strict";

  var ru = {
    "brand.name": "Иникова Полина",
    "brand.subtitle": "2D-художник",
    "nav.projects": "Проекты",
    "nav.sketches": "Скетчи",
    "nav.about": "Обо мне",
    "footer.rights": "© Полина Иникова, 2026. Все права защищены.",
    "back.projects": "← Назад к проектам",
    "projects.title": "Проекты",
    "sketches.title": "Скетчи",
    "about.h1": "Обо мне",
    "about.p1": "Меня зовут Полина, я 2D-художник и аниматор. Люблю создавать разнообразные миры — от фонов и пропсов до персонажей и раскадровок — и работать в разных стилях, находя для каждого проекта свой визуальный язык.",
    "about.p2": "В 2026 году я завершила работу над анимационным короткометражным фильмом «Ковёр» на Свердловской киностудии, где выступила и в качестве режиссёра, и художника-постановщика. Также работала художником по фонам над другими короткометражными фильмами.",
    "about.p3": "В 2022 году получила среднее специальное образование в колледже ВГИК. Сейчас завершаю обучение в университете ВГИК по специальности «художник анимации и компьютерной графики».",
    "about.software.intro": "Владею следующим программным обеспечением:",
    "about.open": "Открыта к интересным проектам.",
    "about.contact.h2": "Контакты",
    "birds-title": "Птицы",
    "carpet-title": "Ковёр",
    "reyneke-fox-title": "Рейнеке-лис",
    "ladies-happiness-title": "Дамское счастье",
    "eden-title": "Эдем",
    "garden-of-the-future-title": "Сад будущего",
    "prince-aquamarine-title": "Принц Аквамарин",
    "spark-of-life-title": "Искра жизни",
    "desc.The-Birds": "Двое афинян вместе с птицами основывают между небом и землёй царство — Тучекукушкин град. За сатирой и фантасмагорией скрывается антиутопия: новый мир, задуманный как свобода, превращается в царство власти, манипуляции и принуждения.",
    "desc.Carpet": "«Ковёр» — детский мультфильм, созданный на Свердловской киностудии, который рассказывает историю о непослушном ковре и одиноком дедушке, об их взаимоотношениях.",
    "desc.Reineke-Fuchs": "Под масками зверей выведено феодальное общество. В центре — хитрый лис Рейнеке, который ловкостью и коварством одерживает верх над противниками и избегает наказания. Поэма представляет собой сатирическую панораму, где зло торжествует, а злодей добивается почета и власти.",
    "desc.The-Ladies-Delight": "Появление первого в мире универмага-гиганта сводит женщин с ума. Витрины, ткани, кружева и запахи превращают их в одержимых, готовых тратить всё до последнего. Однако за блеском этого рая скрывается жестокий механизм, где одни стремительно богатеют, а другие разоряются.",
    "desc.Eden": "Экипаж из шести землян терпит крушение на неизученной планете Эдем. Пытаясь починить корабль, они исследуют чужой мир и сталкиваются с высокоразвитой цивилизацией двутелов.",
    "desc.The-Garden-of-the-Future": "«Сад будущего» — история о мальчике, который с помощью волшебной птицы попадает в разные миры. Каждый из них — иная версия его собственного сада.",
    "desc.Le-Prince-des-Aigues-Marines": "Злая ведьма прокляла принца Аквамарина: любой, кто взглянет на него, погибнет. Принцу приходится преодолеть множество испытаний, чтобы разрушить чары и найти свою возлюбленную, которая томится в Тёмной башне.",
    "desc.Spark-of-Life": "В аду концлагеря, где эсэсовцы издеваются над заключёнными, отнимая у них имя, достоинство и надежду, люди цепляются за последнее, что у них осталось, — за искру жизни.",
    "title.index": "Иникова Полина — художник-постановщик",
    "title.about": "Обо мне — Иникова Полина",
    "title.sketches": "Скетчи — Иникова Полина",
    "title.birds": "Птицы — Иникова Полина",
    "title.carpet": "Ковёр — Иникова Полина",
    "title.reyneke-fox": "Рейнеке-лис — Иникова Полина",
    "title.ladies-happiness": "Дамское счастье — Иникова Полина",
    "title.eden": "Эдем — Иникова Полина",
    "title.garden-of-the-future": "Сад будущего — Иникова Полина",
    "title.prince-aquamarine": "Принц Аквамарин — Иникова Полина",
    "title.spark-of-life": "Искра жизни — Иникова Полина"
  };

  var en = {
    "brand.name": "Polina Inikova",
    "brand.subtitle": "2D Artist",
    "nav.projects": "Projects",
    "nav.sketches": "Sketches",
    "nav.about": "About",
    "footer.rights": "© Polina Inikova, 2026. All rights reserved.",
    "back.projects": "← Back to projects",
    "projects.title": "Projects",
    "sketches.title": "Sketches",
    "about.h1": "About",
    "about.p1": "My name is Polina and I am a 2D artist and animator. I love creating diverse worlds — from backgrounds and props to characters and storyboards — and working across different styles, finding a unique visual language for each project.",
    "about.p2": "In 2026 I completed work on the animated short film \"The Carpet\" at Sverdlovsk Film Studio, where I served as both director and production designer. I have also worked as a background artist on other short films.",
    "about.p3": "In 2022 I received a secondary vocational education at the VGIK College. I am currently completing my studies at VGIK University, specialising in \"animation and computer graphics artist\".",
    "about.software.intro": "I am proficient with the following software:",
    "about.open": "Open to interesting projects.",
    "about.contact.h2": "Contacts",
    "birds-title": "The Birds",
    "carpet-title": "The Carpet",
    "reyneke-fox-title": "Reynard the Fox",
    "ladies-happiness-title": "The Ladies' Delight",
    "eden-title": "Eden",
    "garden-of-the-future-title": "The Garden of the Future",
    "prince-aquamarine-title": "Prince Aquamarine",
    "spark-of-life-title": "The Spark of Life",
    "desc.The-Birds": "Two Athenians, together with the birds, found a kingdom between heaven and earth — Cloudcuckooland. Beneath the satire and phantasmagoria lies a dystopia: a new world conceived as freedom turns into a kingdom of power, manipulation, and coercion.",
    "desc.Carpet": "\"The Carpet\" is a children's animated film created at Sverdlovsk Film Studio. It tells the story of a naughty carpet and a lonely grandfather, and of their relationship.",
    "desc.Reineke-Fuchs": "A feudal society is portrayed behind animal masks. At its centre is the cunning fox Reynard, who wins over his rivals through cleverness and deceit and escapes punishment. The poem is a satirical panorama in which evil triumphs and the villain attains honour and power.",
    "desc.The-Ladies-Delight": "The arrival of the world's first grand department store drives women wild. Shop windows, fabrics, lace, and scents turn them into obsessed customers ready to spend everything. Yet behind the glitter of this paradise hides a ruthless machine in which some grow rich overnight while others are ruined.",
    "desc.Eden": "A crew of six humans crash-lands on the unexplored planet Eden. Trying to repair their ship, they investigate the alien world and encounter a highly advanced civilization of the Two-Bodies.",
    "desc.The-Garden-of-the-Future": "\"The Garden of the Future\" is a story about a boy who, with the help of a magical bird, travels to different worlds. Each of them is another version of his own garden.",
    "desc.Le-Prince-des-Aigues-Marines": "An evil witch cursed Prince Aquamarine: anyone who looks at him dies. The prince must overcome many trials to break the spell and find his beloved, who languishes in the Dark Tower.",
    "desc.Spark-of-Life": "In the hell of a concentration camp, where SS guards torment prisoners, taking their names, dignity, and hope, people cling to the last thing they have left — the spark of life.",
    "title.index": "Polina Inikova — artist",
    "title.about": "About — Polina Inikova",
    "title.sketches": "Sketches — Polina Inikova",
    "title.birds": "The Birds — Polina Inikova",
    "title.carpet": "The Carpet — Polina Inikova",
    "title.reyneke-fox": "Reynard the Fox — Polina Inikova",
    "title.ladies-happiness": "The Ladies' Delight — Polina Inikova",
    "title.eden": "Eden — Polina Inikova",
    "title.garden-of-the-future": "The Garden of the Future — Polina Inikova",
    "title.prince-aquamarine": "Prince Aquamarine — Polina Inikova",
    "title.spark-of-life": "The Spark of Life — Polina Inikova"
  };

  var STORAGE_KEY = "site_lang";
  var defaultLang = "ru";

  function readCookie() {
    var m = document.cookie.match(/(?:^|;\s*)site_lang=([^;]*)/);
    return m ? decodeURIComponent(m[1]) : null;
  }

  function writeCookie(lang) {
    document.cookie = "site_lang=" + encodeURIComponent(lang) +
      "; path=/; max-age=31536000; samesite=lax";
  }

  function currentLang() {
    var saved = null;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      saved = null;
    }
    if (saved !== "en" && saved !== "ru") saved = readCookie();
    return saved === "en" ? "en" : defaultLang;
  }

  function setLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* storage may be unavailable */
    }
    try {
      writeCookie(lang);
    } catch (e) {
      /* ignore */
    }
    applyLang(lang);
  }

  function applyLang(lang) {
    var dict = lang === "en" ? en : ru;
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (dict[key] !== undefined) {
        el.textContent = dict[key];
      }
    });

    document.querySelectorAll("[data-i18n-alt]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-alt");
      if (dict[key] !== undefined) {
        el.setAttribute("alt", dict[key]);
      }
    });

    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-title");
      if (dict[key] !== undefined) {
        document.title = dict[key];
      }
    });

    var btn = document.querySelector(".lang-btn");
    if (btn) {
      if (lang === "en") {
        btn.setAttribute("data-lang", "ru");
        btn.textContent = "EN | РУ";
      } else {
        btn.setAttribute("data-lang", "en");
        btn.textContent = "РУ | EN";
      }
    }
  }

  function initBindings() {
    applyLang(currentLang());
    document.querySelectorAll(".lang-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = btn.getAttribute("data-lang") === "en" ? "en" : "ru";
        setLang(next);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBindings);
  } else {
    initBindings();
  }
})();