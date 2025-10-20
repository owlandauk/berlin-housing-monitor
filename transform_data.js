// n8n Code node to transform spider output for Google Sheets
const spiderOutput = JSON.parse($input.first().json.stdout);

return spiderOutput.map(listing => ({
  json: {
    title: listing.title,
    location: listing.location, 
    details: listing.details,
    price: listing.price,
    link: listing.link,
    image: listing.image,
    scraped_at: new Date().toISOString()
  }
}));
