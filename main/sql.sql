--> Weather
SELECT r.*, w."isDay", w."Temperature", w."Precipitation"
FROM public."Requests" r
INNER JOIN public."Weather" w ON r."RequestID" = w."RequestID";


--> Country
SELECT r.*, c."Country"
FROM public."Requests" r
INNER JOIN public."Country" c ON r."RequestID" = c."RequestID";



--> Locations
SELECT r.*, l."Location", l."Latitude", l."Longitude"
FROM public."Requests" r
INNER JOIN public."Locations" l ON r."RequestID" = l."RequestID";


--> News
SELECT r.*, n."Title", n."PublishedDate", n."Link"
FROM public."Requests" r
INNER JOIN public."News" n ON r."RequestID" = n."RequestID";


--> Timezone
SELECT r.*, t."Timezone", t."Date", t."Time", t."isDST", t."DST"
FROM public."Requests" r
INNER JOIN public."Timezone" t ON r."RequestID" = t."RequestID";
