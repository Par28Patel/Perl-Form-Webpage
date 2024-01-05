#!/usr/bin/perl
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use MIME::Base64;
use strict;
use warnings;

print header;
print start_html(
    -title => 'Response',
    -style => {
        -code => '
            body {
                background-color: rgb(206, 132, 241);
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 400px;
                text-align: left;
            }

            h1 {
                color: rgb(206, 132, 241);
                text-align: center;
            }

            label {
                display: block;
                margin-top: 10px;
                color: #000;
            }

            p {
                margin: 0;
            }

            img {
                max-width: 100%;
                height: auto;
                margin-top: 15px;
                border-radius: 8px;
            }
        '
    }
);

my $toRun = 1;

my $name = param('name');
my $street = param('streetname');
my $city = param('city');
my $province = param('province');
my $photo = param('photo');

my $phone = param('phone');
if ($phone !~ /^\d{10}$/) {
    $toRun = 0;
    print p("Phone number is not valid. It should be 10 digits.");
}

# Validate postal code
my $postal = param('postal');
if ($postal !~ /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/) {
    $toRun = 0;
    print p("Postal code is not valid. It should be in the format A1A 1A1.");
}

# Validate email address
my $email = param('email');
if ($email !~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) {
    $toRun = 0;
    print p("Email address is not valid.");
}

my $photoD;
if ($photo) {
    binmode $photo;
    while (my $bytesR = read($photo, my $buffer, 1024)) {
        $photoD .= $buffer;
    }
}

# Encode the image data to base64
my $encoded = encode_base64($photoD) if $photoD;

if ($toRun) {
    print "<div class='container'>";
    print "<h1>User Information</h1>";
    print "<label for='name'><strong>Name:</strong></label><p>$name</p>";
    print "<label for='street'><strong>Street:</strong></label><p>$street</p>";
    print "<label for='city'><strong>City:</strong></label><p>$city</p>";
    print "<label for='province'><strong>Province:</strong></label><p>$province</p>";
    print "<label for='phone'><strong>Phone:</strong></label><p>$phone</p>";
    print "<label for='postal'><strong>Postal Code:</strong></label><p>$postal</p>";
    print "<label for='email'><strong>Email:</strong></label><p>$email</p>";

    # Display encoded image
    if ($photo) {
        print "<label for='photo'><strong>Photograph:</strong></label>";
        print "<img src='data:image/jpeg;base64,$encoded' alt='User Photograph'>";
    } else {
        print "<p><strong>No photograph uploaded.</strong></p>";
    }
    }


print end_html;
