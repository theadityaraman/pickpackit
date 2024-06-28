function animateOrbit(name, Orbit) {
  const modelViewer = document.querySelector(`#${name}`);
  const orbitCycle = [];
  for (let i = 0; i < Orbit.length; i++) {
    orbitCycle.push(Orbit[i]);
  }
  orbitCycle.push(modelViewer.cameraOrbit);

  setInterval(() => {
    const currentOrbitIndex = orbitCycle.indexOf(modelViewer.cameraOrbit);
    modelViewer.cameraOrbit =
      orbitCycle[(currentOrbitIndex + 1) % orbitCycle.length];
  }, 3000);
}

animateOrbit("orbit-can", [
  "30deg 90deg 5m",
  "60deg 90deg 5m",
  "90deg 90deg 5m",
  "120deg 90deg 5m",
  "150deg 90deg 5m",
  "180deg 90deg 5m",
]);

animateOrbit("orbit-cans", [
  "45deg 90deg 5m",
  "90deg 90deg 5m",
  "135deg 90deg 5m",
  "180deg 90deg 5m",
]);
animateOrbit("orbit-bag", [
  "45deg 90deg 5m",
  "90deg 90deg 5m",
  "135deg 90deg 5m",
  "180deg 90deg 5m",
]);
