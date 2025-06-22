import DashBoardLayoutProvider from "@/provider/dashboard.layout.provider";

import { getDictionary } from "@/app/dictionaries";

const layout = async ({ children, params: { lang } }: { children: React.ReactNode; params: { lang: any } }) => {


  const trans = await getDictionary(lang);

  return (
    <DashBoardLayoutProvider trans={trans}>{children}</DashBoardLayoutProvider>
  );
};

export default layout;
