const MyLogoPlugin = function (system) {
  return {
    components: {
      Logo: () =>
        system.React.createElement("img", {
          alt: "My Logo",
          height: 70,
          src: "/static/logo.png",
        }),
    },
  };
};
