create table line_message_api(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
c_user varchar(100) null,
c_kind varchar(30) null,
c_content varchar(40) null,
c_status varchar(10) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;