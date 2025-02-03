CREATE TABLE IF NOT EXISTS "Pools" (
 "id" serial NOT NULL UNIQUE,
 "name" varchar(255) NOT NULL,
 "address" varchar(255) NOT NULL,
 "capacity" bigint NOT NULL,
 "schedule_id" bigint NOT NULL UNIQUE,
 "is_open" boolean NOT NULL,
 PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Schedule" (
 "id" serial NOT NULL UNIQUE,
 "day" bigint NOT NULL,
 "start_time" time without time zone,
 "end_time" time without time zone,
 PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Users" (
 "id" serial NOT NULL UNIQUE,
 "login" varchar(255) NOT NULL,
 "password" varchar(255) NOT NULL,
 "is_admin" boolean NOT NULL,
 "token" uuid NOT NULL,
 PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Booking" (
 "id" serial NOT NULL UNIQUE,
 "user_id" bigint NOT NULL,
 "pool_id" bigint NOT NULL,
 "start_time" timestamp with time zone NOT NULL,
 "end_time" timestamp with time zone NOT NULL,
 PRIMARY KEY ("id")
);

ALTER TABLE "Pools" ADD CONSTRAINT "Pools_fk4" FOREIGN KEY ("schedule_id") REFERENCES "Schedule"("id");


ALTER TABLE "Booking" ADD CONSTRAINT "Booking_fk1" FOREIGN KEY ("user_id") REFERENCES "Users"("id");

ALTER TABLE "Booking" ADD CONSTRAINT "Booking_fk2" FOREIGN KEY ("pool_id") REFERENCES "Pools"("id");