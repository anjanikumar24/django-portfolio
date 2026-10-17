const loadingScreen = document.getElementById("loadingScreen");
const scrollProgress = document.getElementById("scrollProgress");
const backToTop = document.getElementById("backToTop");

window.addEventListener("load", () => {
  loadingScreen?.classList.add("hide");
});

const updateScrollUi = () => {
  const scrollTop = window.scrollY;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const progress = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;
  if (scrollProgress) scrollProgress.style.width = `${progress}%`;
  backToTop?.classList.toggle("show", scrollTop > 450);
};

window.addEventListener("scroll", updateScrollUi, { passive: true });
backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
updateScrollUi();

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

const progressObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const bar = entry.target;
      bar.style.width = `${bar.dataset.width || 0}%`;
      progressObserver.unobserve(bar);
    }
  });
}, { threshold: 0.4 });

document.querySelectorAll(".progress-bar").forEach((bar) => progressObserver.observe(bar));

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const element = entry.target;
    const target = Number(element.dataset.target || 0);
    const duration = 1200;
    const start = performance.now();
    const tick = (now) => {
      const amount = Math.min((now - start) / duration, 1);
      element.textContent = Math.floor(target * amount).toLocaleString();
      if (amount < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    counterObserver.unobserve(element);
  });
}, { threshold: 0.5 });

document.querySelectorAll(".counter").forEach((counter) => counterObserver.observe(counter));

const typingTarget = document.getElementById("typingText");
if (typingTarget) {
  const phrases = (typingTarget.dataset.text || "").split("|").map((item) => item.trim()).filter(Boolean);
  let phraseIndex = 0;
  let charIndex = 0;
  let deleting = false;
  const type = () => {
    if (!phrases.length) return;
    const phrase = phrases[phraseIndex];
    typingTarget.textContent = phrase.slice(0, charIndex);
    if (!deleting && charIndex < phrase.length) charIndex += 1;
    else if (deleting && charIndex > 0) charIndex -= 1;
    else if (!deleting) deleting = true;
    else {
      deleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
    }
    const delay = deleting ? 45 : 80;
    setTimeout(type, charIndex === phrase.length ? 950 : delay);
  };
  type();
}
