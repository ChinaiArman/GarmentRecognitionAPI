// Change logo of Swagger UI
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

// Make filter bar search for endpoint keywords
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

// Add a filter bar with new placeholder text
const NewFilterPlugin = function (system) {
  return {
    wrapComponents: {
      FilterContainer: (Original, system) =>
        class NewFilterContainer extends system.React.Component {
          // static propTypes = {
          //   specSelectors: PropTypes.object.isRequired,
          //   layoutSelectors: PropTypes.object.isRequired,
          //   layoutActions: PropTypes.object.isRequired,
          //   getComponent: PropTypes.func.isRequired,
          // }

          onFilterChange = (e) => {
            const {
              target: { value },
            } = e;
            this.props.layoutActions.updateFilter(value);
          };

          render() {
            const { specSelectors, layoutSelectors, getComponent } = this.props;
            const Col = getComponent("Col");

            const isLoading = specSelectors.loadingStatus() === "loading";
            const isFailed = specSelectors.loadingStatus() === "failed";
            const filter = layoutSelectors.currentFilter();

            const classNames = ["operation-filter-input"];
            if (isFailed) classNames.push("failed");
            if (isLoading) classNames.push("loading");

            return system.React.createElement(
              "div",
              null,
              system.React.createElement(
                "div",
                { className: "filter-container" },
                system.React.createElement(
                  Col,
                  { className: "filter wrapper", mobile: 12 },
                  system.React.createElement("input", {
                    className: classNames.join(" "),
                    placeholder: "Filter by endpoint keywords",
                    type: "text",
                    onChange: this.onFilterChange,
                    value: typeof filter === "string" ? filter : "",
                    disabled: isLoading,
                  })
                )
              )
            );
          }
        },
    },
  };
};
