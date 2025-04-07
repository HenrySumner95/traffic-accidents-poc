const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#map-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Define the zoom behavior
const zoom = d3.zoom()
    .scaleExtent([1, 8])  // Set the zoom scale extent (min and max zoom levels)
    .on("zoom", zoomed);  // Event handler for zooming

// Apply the zoom behavior to the SVG
svg.call(zoom);

// Zoom function
function zoomed(event) {
svg.selectAll("path")
    .attr("transform", event.transform);  // Apply the zoom transformation to each country path
}

const projection = d3.geoMercator()
    .scale(130)
    .translate([width / 2, height / 1.5]);

const tooltip = d3.select("body")
.append("div")
.attr("class", "tooltip") // style this in CSS
.style("position", "absolute")
.style("padding", "6px 10px")
.style("background", "rgba(0,0,0,0.7)")
.style("color", "#fff")
.style("border-radius", "4px")
.style("pointer-events", "none")
.style("font-size", "12px")


const path = d3.geoPath().projection(projection);
const geojsonUrl = "https://gist.githubusercontent.com/HenrySumner95/454fe49ee7b7b68b96fa4c9ddeed8fdd/raw/07c5009be39809cee3ad611abad6cf5576b7e9e2/world_countries.geojson"

fetch("https://gist.githubusercontent.com/HenrySumner95/76b0e4d636b9bc1c2169c175d50c8c9e/raw/2447bae6624633ae5917b0292276d066bf1a8a60/traffic_accidents_colours.json")
        .then(response => response.json())
        .then(colours => {
            d3.json(geojsonUrl).then(function(data) {
            svg.selectAll("path")
            .data(data.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("stroke", "black")
            .attr("fill", d => {
                const name = d.properties.admin;
                console.log(name)
                return colours[name] || "#fff"; // default if not found
                })
            .attr("stroke-width", 0.5)
            .on("mouseover", function (event, d) {
                tooltip
                .style("opacity", 1)
                .html(`<strong>${d.properties.admin}</strong>`);

                const currentFill = d3.select(this).attr("fill");
                const brighter = d3.color(currentFill).brighter(0.5); // you can adjust the number

                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr("fill", brighter);
            })
            .on("mousemove", function (event) {
                tooltip
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function (event, d) {
                tooltip.style("opacity", 0);
                const name = d.properties.admin;
                const originalColor = colours[name] || "#fff";

                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr("fill", originalColor);
            })
            .on("click", function(event, d) {
                const [[x0, y0], [x1, y1]] = path.bounds(d);
                event.stopPropagation();
                svg.transition().duration(750).call(
                zoom.transform,
                d3.zoomIdentity
                    .translate(width / 2, height / 2)
                    .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
                    .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
                d3.pointer(event, svg.node())
                );
            });
        }).catch(function(error) {
        console.error("Error loading GeoJSON:", error);
        });
        });