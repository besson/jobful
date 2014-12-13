var map = new Datamap({
  element: document.getElementById('container'),
    scope: 'usa',
    geographyConfig: {
      highlightOnHover: false,
      popupOnHover: false
    },

    fills: {
      'SDE': '#1f77b4',
      'SDEI': '#1f77b4',
      'CSE': '#1f77b4',
      'TE': '#9467bd',
      'TPM': '#FF6666',
      'SDM': '#6591D5',
      'EOT': '#FFFF00',
      'SPM': '#FFA500',
      'EOT': '#FFA500',
      defaultFill: '#613f69'
    }
});

d3.json("map/bubbles", function(error, json) {
  if (error) return console.warn(error);

  jobs = json;
  map.bubbles(jobs, {
    popupTemplate: function (geo, data) { 
      return ['<div class="hoverinfo">' +  data.name,
    '<br/>' + data.radius + ' positions',
    '<br/>state: ' + data.state,
    '</div>'].join('');
    }
  });
});
