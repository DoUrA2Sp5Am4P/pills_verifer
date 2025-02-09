# Read each line from tablets.txt
$names = Get-Content -Path "tablets.txt"

# Base URL for downloading
$baseUrl = "http://qrcoder.ru/code/?{0}&2&0"

# Loop through each name
foreach ($name in $names) {
    # Format the URL
    $url = $baseUrl -f $name
    
    # Define the output file name
    $outputFile = "{0}.gif" -f $name
    
    # Download the file using wget
    wget $url -OutFile $outputFile
}