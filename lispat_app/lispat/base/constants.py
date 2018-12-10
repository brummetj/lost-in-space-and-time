DESIRED_TERMS = [
    "asset",
    "authentication",
    "authenticity",
    "authorization",
    "availability",
    "confidentiality",
    "configuration",
    "cryptographically strong",
    "cybersecurity",
    "cybersecurity bill of materials",
    "cbom",
    "denial of service",
    "encryption",
    "end of support",
    "integrity",
    "jitter",
    "life-cycle",
    "malware",
    "patchability",
    "updatability",
    "patient harm",
    "privileged user",
    "quality of service",
    "risk",
    "risk analysis",
    "trustworthy device",
    "regulations",
    "regulatory",
    "regulation"
]

DESIRED_PHRASE = [
    "shall",
    "required",
    "requires",
    "must",
    "need",
    "has"
]

css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""

JAVASCRIPT = """
mpld3.register_plugin("clickinfo", ClickInfo);
ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
ClickInfo.prototype.constructor = ClickInfo;
ClickInfo.prototype.requiredProps = ["id"];
function ClickInfo(fig, props){
    mpld3.Plugin.call(this, fig, props);
};

ClickInfo.prototype.draw = function(){
    var obj = mpld3.get_element(this.props.id);
    obj.elements().on("mousedown",
                      function(d, i){alert("clicked on points[" + i + "]");});
}
"""