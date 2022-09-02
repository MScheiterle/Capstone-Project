var renderer, camera, scene, controls;

let windowHalfY = window.innerHeight / 2;
var Globe;

const EARTH_RADIUS_KM = 6371; // km
const SAT_SIZE = 80; // km
const TIME_STEP = 3 * 1000; // per frame

var myCanvas = document.getElementById("globe");

var loader = new THREE.STLLoader();

init();
initGlobe();
onWindowResize();
animate();

// SECTION Initializing core ThreeJS elements
function init() {
  // Initialize renderer
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    canvas: myCanvas,
    alpha: true,
  });
  renderer.setSize(windowHalfY, windowHalfY);

  // Initialize scene, light
  scene = new THREE.Scene();
  scene.add(new THREE.AmbientLight(0xbbbbbb, 0.3));

  // Initialize camera, light
  camera = new THREE.PerspectiveCamera();
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  var dLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dLight.position.set(-800, 2000, 400);
  camera.add(dLight);

  var dLight1 = new THREE.DirectionalLight(0x7982f6, 1);
  dLight1.position.set(-200, 500, 200);
  camera.add(dLight1);

  var dLight2 = new THREE.PointLight(0x8566cc, 0.5);
  dLight2.position.set(-200, 500, 200);
  camera.add(dLight2);

  camera.position.z = 270;
  camera.position.x = 0;
  camera.position.y = 0;

  scene.add(camera);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.update();
  controls.enablePan = false;
  controls.enableZoom = false;
  controls.enableDamping = true;
  controls.dampingFactor = 0.005;

  window.addEventListener("resize", onWindowResize, false);
}

// SECTION Globe
function initGlobe() {
  fetch("./static/assets/geography-data.json")
    .then((response) => {
      return response.json();
    })
    .then((countries) => {
      // Initialize the Globe
      Globe = new ThreeGlobe({
        waitForGlobeReady: true,
        animateIn: true,
      })
        .hexPolygonsData(countries[0].features)
        .hexPolygonResolution(3)
        .hexPolygonMargin(0.7)
        .showAtmosphere(true)
        .atmosphereColor("#3a228a")
        .atmosphereAltitude(0.15)
        .hexPolygonColor((e) => {
          return "rgba(255,255,255, 0.7)";
        });

      fetch("./static/assets/people-data.json")
        .then((response) => {
          return response.json();
        })
        .then((airportHistory) => {
          setTimeout(() => {
            Globe.pointsData(airportHistory.people)
              .pointColor(() => "#ffffff")
              .pointsMerge(true)
              .pointAltitude(0.09)
              .pointRadius(0.05);
          }, 500);
        });

      const globeMaterial = Globe.globeMaterial();
      globeMaterial.color = new THREE.Color(0x3a228a);
      globeMaterial.emissive = new THREE.Color(0x220038);
      globeMaterial.emissiveIntensity = 0.1;
      globeMaterial.shininess = 0.7;

      Globe.name = "Globe";
      scene.add(Globe);

      const satMaterial = new THREE.MeshStandardMaterial();
      loader.load("./static/assets/discord.stl", function (discordSatGeometry) {
        loader.load(
          "./static/assets/XboxOneLogo.stl",
          function (xboxSatGeometry) {
            loader.load("./static/assets/PS.stl", function (psSatGeometry) {
              geometries = [discordSatGeometry, xboxSatGeometry, psSatGeometry];
              geometries.map((geometry) => geometry.scale(0.25, 0.25, 0.25));
              Globe.objectThreeObject(
                () =>
                  new THREE.Mesh(
                    geometries[Math.floor(Math.random() * geometries.length)],
                    satMaterial
                  )
              );
            });
          }
        );
      });

      fetch("./static/assets/space-track-leo.txt")
        .then((r) => r.text())
        .then((rawData) => {
          const tleData = rawData
            .replace(/\r/g, "")
            .split(/\n(?=[^12])/)
            .map((tle) => tle.split("\n"));
          const satData = tleData.map(([name, ...tle]) => ({
            satrec: satellite.twoline2satrec(...tle),
            name: name.trim().replace(/^0 /, ""),
          }));

          // time ticker
          let time = new Date();
          (function frameTicker() {
            requestAnimationFrame(frameTicker);

            time = new Date(+time + TIME_STEP);

            // Update satellite positions
            const gmst = satellite.gstime(time);
            satData.forEach((d) => {
              const eci = satellite.propagate(d.satrec, time);
              if (eci.position) {
                const gdPos = satellite.eciToGeodetic(eci.position, gmst);
                d.lat = satellite.radiansToDegrees(gdPos.latitude);
                d.lng = satellite.radiansToDegrees(gdPos.longitude);
                d.alt = gdPos.height / EARTH_RADIUS_KM;
                try {
                  d.__threeObj.lookAt(0, 0, 0);
                } catch {}
              }
            });

            Globe.objectsData(satData);
          })();
        });
    });
}

function onWindowResize() {
  camera.aspect = window.innerHeight / window.innerHeight;
  camera.updateProjectionMatrix();
  windowHalfY = window.innerHeight / 1.5;
  renderer.setSize(windowHalfY, windowHalfY);
}

function animate() {
  try {
    let Globe = scene.getObjectByName("Globe");
    Globe.rotation.y += 0.0005;
  } catch {}
  controls.update();
  camera.lookAt(scene.position);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
