export function createPageUrl(pageName) {
  const pageMap = {
    Home: "/",
    Models: "/models",
    History: "/history",
  };
  
  return pageMap[pageName] || "/";
}


