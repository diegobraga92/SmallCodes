/*
TryFrom<&str> for Domain Type
--------------------------------------------------------
Example:

struct Email(String);

Validate format.

Senior signal:
- Custom error enum
- From / TryFrom traits
- Encapsulation of invariants
*/
use std::convert::TryFrom;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Email(String);

impl Email {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum EmailError {
    Empty,
    MissingAt,
    MissingDomain,
}

impl fmt::Display for EmailError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            EmailError::Empty => write!(f, "email cannot be empty"),
            EmailError::MissingAt => write!(f, "email missing @"),
            EmailError::MissingDomain => write!(f, "email missing domain"),
        }
    }
}

impl std::error::Error for EmailError {}

impl TryFrom<&str> for Email {
    type Error = EmailError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        if value.trim().is_empty() {
            return Err(EmailError::Empty);
        }

        let (local, domain) = value.split_once('@').ok_or(EmailError::MissingAt)?;

        if domain.is_empty() || !domain.contains('.') {
            return Err(EmailError::MissingDomain);
        }

        if local.is_empty() {
            return Err(EmailError::MissingAt);
        }

        Ok(Email(value.to_string()))
    }
}

fn main() {
    println!("Hello, world!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_email() {
        let email = Email::try_from("john@doe.com").unwrap();
        assert_eq!(email.as_str(), "john@doe.com");
    }

    #[test]
    fn empty_email_fails() {
        let err = Email::try_from("").unwrap_err();
        assert_eq!(err, EmailError::Empty);
    }

    #[test]
    fn missing_at_fails() {
        let err = Email::try_from("johndoe.com").unwrap_err();
        assert_eq!(err, EmailError::MissingAt);
    }

    #[test]
    fn missing_domain_fails() {
        let err = Email::try_from("john@doe").unwrap_err();
        assert_eq!(err, EmailError::MissingDomain);
    }

    #[test]
    fn missing_local_part_fails() {
        let err = Email::try_from("@doe.com").unwrap_err();
        assert_eq!(err, EmailError::MissingAt);
    }
}
