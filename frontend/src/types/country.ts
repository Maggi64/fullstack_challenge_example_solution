export type CountriesResponse = {
    countries: Country[];
    total:     number;
}

export type Country = {
    code:       number;
    name:       string;
    region:     string;
    languages:  string[];
    population: number;
    favorite:   boolean;
}