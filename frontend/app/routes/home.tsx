import type { Route } from "./+types/home";
import App from "../../src/App";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Sacred Learning Center - Talk Finder" },
    {
      name: "description",
      content: "Welcome to Sacred Learning Center - Talk Finder!",
    },
  ];
}

export default function Home() {
  return <App />;
  // return <Welcome />;
}
