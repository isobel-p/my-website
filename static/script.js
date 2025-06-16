document.addEventListener("DOMContentLoaded", function() {
  gsap.registerPlugin(SplitText, Draggable, InertiaPlugin);

  let split = SplitText.create(".split", { type: "words, chars" });

  gsap.from(split.chars, {
    duration: 1, 
    y: 100,
    autoAlpha: 0,
    stagger: 0.05
  });

  Draggable.create("#python", { inertia: true, bounds:document.getElementsByClassName("content") });
  Draggable.create("#html", { inertia: true, bounds:document.getElementsByClassName("content") });
  Draggable.create("#css", { inertia: true, bounds:document.getElementsByClassName("content") });
  Draggable.create("#js", { inertia: true, bounds:document.getElementsByClassName("content") });
  Draggable.create("#c",  { inertia: true, bounds:document.getElementsByClassName("content") });
});
