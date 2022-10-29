# cloud-datastore-ttl

Sample scripts to test out the TTL feature of Cloud Datastore

## Set TTL using a date/time field
- `Transaction` is the Kind
- `expiry_timestamp` is the field name used to make the entity expire
```
gcloud beta firestore fields ttls update expiry_timestamp --collection-group=Transaction --enable-ttl
```

## Useful GQL
Find all transactions belong to a single customer entity
```graql
SELECT * FROM Transaction
WHERE __key__ HAS ANCESTOR Key(Customer, "34d128f5b3dede622e107438fbefabdf0519ebab21ac7b6f2075f974d09ce524_12346")
```

