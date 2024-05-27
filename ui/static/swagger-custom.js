const MyLogoPlugin = function (system) {
  return {
    components: {
      Logo: () =>
        system.React.createElement("img", {
          alt: "My Logo",
          height: 50,
          src: "/static/logo.png",
        }),
    },
  };
};

const AdvancedFilterPlugin = function (system) {
  return {
    fn: {
      opsFilter: function (taggedOps, phrase) {
        phrase = phrase.toLowerCase();
        //first filter out all actions that don't meet the search criteria
        var filteredActions = taggedOps.map((tagObj) => {
          tagObj._root.entries[1][1] = tagObj._root.entries[1][1].filter(
            (operationObj) => {
              var op = JSON.parse(JSON.stringify(operationObj));
              var summary = "";
              var description = "";
              if (typeof op.operation.summary !== "undefined") {
                summary = JSON.stringify(op.operation.summary).toLowerCase();
              }
              if (typeof op.operation.description !== "undefined") {
                description = JSON.stringify(
                  op.operation.description
                ).toLowerCase();
              }
              if (
                op.path.toLowerCase().indexOf(phrase) === -1 &&
                summary.indexOf(phrase) === -1 &&
                description.indexOf(phrase) === -1
              ) {
                return false;
              } else {
                return true;
              }
            }
          );
          return tagObj;
        });
        //then filter any Tags with no actions remaining
        return filteredActions.filter((tagObj) => {
          return tagObj._root.entries[1][1].size > 0;
        });
      },
    },
  };
};
